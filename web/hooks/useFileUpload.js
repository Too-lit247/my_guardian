import { useState } from 'react';

export const useFileUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);

  const uploadFile = async (file, uploadType = 'general') => {
    if (!file) {
      setError('No file selected');
      return null;
    }

    setUploading(true);
    setError(null);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', uploadType);

      // Simulate upload progress (since fetch doesn't provide real progress)
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 100);

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Upload failed');
      }

      const result = await response.json();
      
      setUploading(false);
      setUploadProgress(0);
      
      return result;

    } catch (err) {
      setError(err.message);
      setUploading(false);
      setUploadProgress(0);
      return null;
    }
  };

  const uploadMultipleFiles = async (files, uploadType = 'general') => {
    const results = [];
    
    for (const file of files) {
      const result = await uploadFile(file, uploadType);
      if (result) {
        results.push(result);
      }
    }
    
    return results;
  };

  return {
    uploadFile,
    uploadMultipleFiles,
    uploading,
    uploadProgress,
    error,
    clearError: () => setError(null)
  };
};

// Utility functions for file validation
export const validateFile = (file, allowedTypes = [], maxSize = 10 * 1024 * 1024) => {
  const errors = [];

  // Check file type
  if (allowedTypes.length > 0) {
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const isValidType = allowedTypes.some(type => 
      type.toLowerCase().includes(fileExtension)
    );
    
    if (!isValidType) {
      errors.push(`Invalid file type. Allowed: ${allowedTypes.join(', ')}`);
    }
  }

  // Check file size
  if (file.size > maxSize) {
    const maxSizeMB = Math.round(maxSize / (1024 * 1024));
    errors.push(`File too large. Maximum size is ${maxSizeMB}MB`);
  }

  return {
    isValid: errors.length === 0,
    errors
  };
};

// File type presets
export const FILE_TYPES = {
  DOCUMENTS: ['.pdf', '.doc', '.docx'],
  IMAGES: ['.jpg', '.jpeg', '.png', '.gif'],
  AUDIO: ['.wav', '.mp3', '.m4a'],
  ALL_MEDIA: ['.pdf', '.jpg', '.jpeg', '.png', '.wav', '.mp3', '.m4a']
};
