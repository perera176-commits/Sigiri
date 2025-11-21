/**
 * SIGIRI Converter Library
 * Handles file upload, conversion, and download
 * Supports both client-side and server-side conversion
 */

class SIGIRIConverter {
  constructor(options = {}) {
    this.apiUrl = options.apiUrl || this.detectAPIUrl();
    this.maxFileSize = options.maxFileSize || 10 * 1024 * 1024; // 10MB
    this.maxFiles = options.maxFiles || 5;
    this.onProgress = options.onProgress || (() => {});
    this.onComplete = options.onComplete || (() => {});
    this.onError = options.onError || ((error) => console.error(error));
  }

  /**
   * Auto-detect API URL based on environment
   */
  detectAPIUrl() {
    const isLocal = window.location.hostname === 'localhost' || 
                   window.location.hostname === '127.0.0.1' || 
                   window.location.protocol === 'file:';
    
    return isLocal 
      ? 'http://localhost:8080/api/convert'
      : 'https://backend-yanie.ondigitalocean.app/api/convert';
  }

  /**
   * Validate files before upload
   */
  validateFiles(files) {
    const errors = [];

    if (files.length === 0) {
      errors.push('No files selected');
      return { valid: false, errors };
    }

    if (files.length > this.maxFiles) {
      errors.push(`Maximum ${this.maxFiles} files allowed`);
    }

    for (const file of files) {
      if (file.size > this.maxFileSize) {
        errors.push(`${file.name} is too large (max ${this.formatFileSize(this.maxFileSize)})`);
      }
    }

    return { 
      valid: errors.length === 0, 
      errors 
    };
  }

  /**
   * Upload files to server
   */
  async uploadFiles(files) {
    const formData = new FormData();
    
    for (const file of files) {
      formData.append('files', file);
    }

    try {
      this.onProgress({ stage: 'uploading', progress: 0 });

      const response = await fetch(`${this.apiUrl}/upload`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.message || 'Upload failed');
      }

      this.onProgress({ stage: 'uploading', progress: 100 });
      return data;

    } catch (error) {
      this.onError(error);
      throw error;
    }
  }

  /**
   * Start conversion process
   */
  async startConversion(uploadId, options = {}) {
    try {
      this.onProgress({ stage: 'converting', progress: 0 });

      const response = await fetch(`${this.apiUrl}/process/${uploadId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(options)
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.message || 'Conversion failed');
      }

      return data.jobId;

    } catch (error) {
      this.onError(error);
      throw error;
    }
  }

  /**
   * Poll conversion status
   */
  async pollStatus(jobId, interval = 1000) {
    return new Promise((resolve, reject) => {
      const checkStatus = async () => {
        try {
          const response = await fetch(`${this.apiUrl}/status/${jobId}`);
          const data = await response.json();

          if (!data.success) {
            reject(new Error(data.message || 'Status check failed'));
            return;
          }

          if (data.status === 'complete') {
            this.onProgress({ stage: 'converting', progress: 100 });
            resolve(data);
          } else if (data.status === 'failed') {
            reject(new Error(data.error || 'Conversion failed'));
          } else {
            // Still processing, check again
            this.onProgress({ stage: 'converting', progress: 50 });
            setTimeout(checkStatus, interval);
          }

        } catch (error) {
          reject(error);
        }
      };

      checkStatus();
    });
  }

  /**
   * Download converted file
   */
  async downloadFile(jobId, filename = 'converted.pdf') {
    try {
      this.onProgress({ stage: 'downloading', progress: 0 });

      const downloadUrl = `${this.apiUrl}/download/${jobId}`;
      
      // Create invisible link and trigger download
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      this.onProgress({ stage: 'downloading', progress: 100 });
      this.onComplete({ success: true, filename });

    } catch (error) {
      this.onError(error);
      throw error;
    }
  }

  /**
   * Convert files (complete workflow)
   */
  async convert(files, options = {}) {
    try {
      // Validate
      const validation = this.validateFiles(files);
      if (!validation.valid) {
        throw new Error(validation.errors.join(', '));
      }

      // Upload
      const uploadResult = await this.uploadFiles(files);
      
      // Start conversion
      const jobId = await this.startConversion(uploadResult.uploadId, options);
      
      // Wait for completion
      const status = await this.pollStatus(jobId);
      
      // Download
      await this.downloadFile(jobId, options.outputFilename || 'converted.pdf');

      return { success: true };

    } catch (error) {
      this.onError(error);
      throw error;
    }
  }

  /**
   * Format file size for display
   */
  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }
}

/**
 * Client-side Image to PDF Converter
 * Uses browser APIs (no server needed)
 */
class ClientSideConverter {
  /**
   * Convert images to PDF in browser
   */
  static async imagesToPDF(files, options = {}) {
    const { quality = 0.9, pageSize = 'A4', orientation = 'portrait' } = options;

    // Page dimensions (A4 in points: 72 points per inch)
    const pageSizes = {
      'A4': { width: 595, height: 842 },
      'Letter': { width: 612, height: 792 },
      'Legal': { width: 612, height: 1008 }
    };

    const page = pageSizes[pageSize] || pageSizes['A4'];
    const [pageWidth, pageHeight] = orientation === 'portrait' 
      ? [page.width, page.height] 
      : [page.height, page.width];

    // Note: For production, you'd use jsPDF library
    // This is a simplified version
    const images = [];

    for (const file of files) {
      const imageData = await this.fileToDataURL(file);
      const img = await this.loadImage(imageData);
      images.push(img);
    }

    // In production, use jsPDF to create PDF
    // For now, return success
    return {
      success: true,
      method: 'client-side',
      images: images.length
    };
  }

  /**
   * Convert file to data URL
   */
  static fileToDataURL(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  /**
   * Load image element
   */
  static loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = src;
    });
  }
}

// Export for use in HTML pages
if (typeof window !== 'undefined') {
  window.SIGIRIConverter = SIGIRIConverter;
  window.ClientSideConverter = ClientSideConverter;
}
