const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const sharp = require('sharp');
const { PDFDocument } = require('pdf-lib');
const { v4: uuidv4 } = require('uuid');

// Create directories if they don't exist
const uploadDir = path.join(__dirname, '../uploads');
const processedDir = path.join(__dirname, '../processed');

const ensureDirectories = async () => {
  try {
    await fs.mkdir(uploadDir, { recursive: true });
    await fs.mkdir(processedDir, { recursive: true });
  } catch (error) {
    console.error('Error creating directories:', error);
  }
};
ensureDirectories();

// Configure multer for file upload
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    await ensureDirectories();
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

const fileFilter = (req, file, cb) => {
  // Accept images only
  const allowedTypes = /jpeg|jpg|png|gif|bmp|webp|tiff|heic|heif/;
  const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
  const mimetype = allowedTypes.test(file.mimetype);

  if (mimetype && extname) {
    return cb(null, true);
  } else {
    cb(new Error('Only image files are allowed!'));
  }
};

const upload = multer({
  storage: storage,
  limits: { 
    fileSize: 10 * 1024 * 1024, // 10MB limit for free tier
    files: 5 // Max 5 files for free tier
  },
  fileFilter: fileFilter
});

// Store conversion jobs in memory (use Redis in production)
const conversionJobs = new Map();

/**
 * @route   POST /api/convert/upload
 * @desc    Upload files for conversion
 * @access  Public
 */
router.post('/upload', upload.array('files', 5), async (req, res) => {
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ 
        success: false, 
        message: 'No files uploaded' 
      });
    }

    const uploadId = uuidv4();
    const files = req.files.map(file => ({
      id: uuidv4(),
      originalName: file.originalname,
      filename: file.filename,
      path: file.path,
      size: file.size,
      mimetype: file.mimetype
    }));

    // Store upload info
    conversionJobs.set(uploadId, {
      uploadId,
      files,
      status: 'uploaded',
      createdAt: new Date()
    });

    res.json({
      success: true,
      uploadId,
      files: files.map(f => ({
        id: f.id,
        name: f.originalName,
        size: f.size
      }))
    });

  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ 
      success: false, 
      message: error.message 
    });
  }
});

/**
 * @route   POST /api/convert/process/:uploadId
 * @desc    Process conversion (JPG/PNG/etc to PDF)
 * @access  Public
 */
router.post('/process/:uploadId', async (req, res) => {
  try {
    const { uploadId } = req.params;
    const { format = 'pdf', quality = 90, pageSize = 'A4', orientation = 'portrait' } = req.body;

    const job = conversionJobs.get(uploadId);
    if (!job) {
      return res.status(404).json({ 
        success: false, 
        message: 'Upload not found' 
      });
    }

    // Update job status
    job.status = 'processing';
    job.format = format;
    job.options = { quality, pageSize, orientation };
    conversionJobs.set(uploadId, job);

    // Start conversion asynchronously
    convertImagesToPDF(uploadId, job.files, { quality, pageSize, orientation })
      .then(outputPath => {
        job.status = 'complete';
        job.outputPath = outputPath;
        job.completedAt = new Date();
        conversionJobs.set(uploadId, job);
      })
      .catch(error => {
        job.status = 'failed';
        job.error = error.message;
        conversionJobs.set(uploadId, job);
      });

    res.json({
      success: true,
      jobId: uploadId,
      status: 'processing',
      message: 'Conversion started'
    });

  } catch (error) {
    console.error('Process error:', error);
    res.status(500).json({ 
      success: false, 
      message: error.message 
    });
  }
});

/**
 * @route   GET /api/convert/status/:jobId
 * @desc    Check conversion status
 * @access  Public
 */
router.get('/status/:jobId', (req, res) => {
  try {
    const { jobId } = req.params;
    const job = conversionJobs.get(jobId);

    if (!job) {
      return res.status(404).json({ 
        success: false, 
        message: 'Job not found' 
      });
    }

    res.json({
      success: true,
      status: job.status,
      fileCount: job.files.length,
      downloadUrl: job.status === 'complete' ? `/api/convert/download/${jobId}` : null,
      error: job.error || null
    });

  } catch (error) {
    console.error('Status check error:', error);
    res.status(500).json({ 
      success: false, 
      message: error.message 
    });
  }
});

/**
 * @route   GET /api/convert/download/:jobId
 * @desc    Download converted file
 * @access  Public
 */
router.get('/download/:jobId', async (req, res) => {
  try {
    const { jobId } = req.params;
    const job = conversionJobs.get(jobId);

    if (!job) {
      return res.status(404).json({ 
        success: false, 
        message: 'Job not found' 
      });
    }

    if (job.status !== 'complete') {
      return res.status(400).json({ 
        success: false, 
        message: 'Conversion not complete yet' 
      });
    }

    // Send file
    res.download(job.outputPath, 'converted.pdf', async (err) => {
      if (err) {
        console.error('Download error:', err);
      }
      
      // Clean up files after download
      try {
        // Delete uploaded files
        for (const file of job.files) {
          await fs.unlink(file.path).catch(() => {});
        }
        // Delete processed file
        await fs.unlink(job.outputPath).catch(() => {});
        // Remove job from memory
        conversionJobs.delete(jobId);
      } catch (cleanupError) {
        console.error('Cleanup error:', cleanupError);
      }
    });

  } catch (error) {
    console.error('Download error:', error);
    res.status(500).json({ 
      success: false, 
      message: error.message 
    });
  }
});

/**
 * Convert images to PDF
 * @param {string} jobId - Job ID
 * @param {Array} files - Array of file objects
 * @param {Object} options - Conversion options
 */
async function convertImagesToPDF(jobId, files, options = {}) {
  const { quality = 90, pageSize = 'A4', orientation = 'portrait' } = options;

  // Page size dimensions in points (1 point = 1/72 inch)
  const pageSizes = {
    'A4': orientation === 'portrait' ? [595, 842] : [842, 595],
    'Letter': orientation === 'portrait' ? [612, 792] : [792, 612],
    'Legal': orientation === 'portrait' ? [612, 1008] : [1008, 612]
  };

  const [pageWidth, pageHeight] = pageSizes[pageSize] || pageSizes['A4'];

  // Create a new PDF document
  const pdfDoc = await PDFDocument.create();

  // Process each image
  for (const file of files) {
    try {
      // Read and process image with Sharp
      const imageBuffer = await sharp(file.path)
        .jpeg({ quality: parseInt(quality) })
        .toBuffer();

      // Embed image in PDF
      const image = await pdfDoc.embedJpg(imageBuffer);
      const imageDims = image.scale(1);

      // Calculate scaling to fit page
      const scaleX = pageWidth / imageDims.width;
      const scaleY = pageHeight / imageDims.height;
      const scale = Math.min(scaleX, scaleY, 1); // Don't upscale

      const scaledWidth = imageDims.width * scale;
      const scaledHeight = imageDims.height * scale;

      // Center image on page
      const x = (pageWidth - scaledWidth) / 2;
      const y = (pageHeight - scaledHeight) / 2;

      // Add page and draw image
      const page = pdfDoc.addPage([pageWidth, pageHeight]);
      page.drawImage(image, {
        x,
        y,
        width: scaledWidth,
        height: scaledHeight
      });

    } catch (error) {
      console.error(`Error processing file ${file.originalName}:`, error);
      throw new Error(`Failed to process ${file.originalName}: ${error.message}`);
    }
  }

  // Save PDF
  const pdfBytes = await pdfDoc.save();
  const outputPath = path.join(processedDir, `${jobId}.pdf`);
  await fs.writeFile(outputPath, pdfBytes);

  return outputPath;
}

/**
 * Cleanup old files (run periodically)
 */
async function cleanupOldFiles() {
  const maxAge = 60 * 60 * 1000; // 1 hour
  const now = Date.now();

  for (const [jobId, job] of conversionJobs.entries()) {
    const age = now - job.createdAt.getTime();
    
    if (age > maxAge) {
      // Delete files
      for (const file of job.files) {
        await fs.unlink(file.path).catch(() => {});
      }
      if (job.outputPath) {
        await fs.unlink(job.outputPath).catch(() => {});
      }
      
      // Remove job
      conversionJobs.delete(jobId);
    }
  }
}

// Run cleanup every 15 minutes
setInterval(cleanupOldFiles, 15 * 60 * 1000);

module.exports = router;
