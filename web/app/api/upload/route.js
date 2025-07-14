import { NextRequest, NextResponse } from 'next/server';
import { writeFile, mkdir } from 'fs/promises';
import path from 'path';

export async function POST(request) {
  try {
    const formData = await request.formData();
    const file = formData.get('file');
    const uploadType = formData.get('type') || 'general'; // registration_docs, department_docs, audio_samples

    if (!file) {
      return NextResponse.json(
        { error: 'No file uploaded' },
        { status: 400 }
      );
    }

    // Validate file type
    const allowedTypes = {
      'registration_docs': ['.pdf', '.jpg', '.jpeg', '.png'],
      'department_docs': ['.pdf', '.jpg', '.jpeg', '.png'],
      'audio_samples': ['.wav', '.mp3', '.m4a'],
      'general': ['.pdf', '.jpg', '.jpeg', '.png', '.wav', '.mp3', '.m4a']
    };

    const fileExtension = path.extname(file.name).toLowerCase();
    const validTypes = allowedTypes[uploadType] || allowedTypes['general'];
    
    if (!validTypes.includes(fileExtension)) {
      return NextResponse.json(
        { error: `Invalid file type. Allowed: ${validTypes.join(', ')}` },
        { status: 400 }
      );
    }

    // Validate file size (10MB max)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File too large. Maximum size is 10MB' },
        { status: 400 }
      );
    }

    // Create unique filename
    const timestamp = Date.now();
    const randomString = Math.random().toString(36).substring(2, 8);
    const fileName = `${timestamp}_${randomString}_${file.name}`;

    // Create upload directory structure
    const uploadDir = path.join(process.cwd(), 'public', 'uploads', uploadType);
    
    try {
      await mkdir(uploadDir, { recursive: true });
    } catch (error) {
      // Directory might already exist, that's okay
    }

    // Save file
    const filePath = path.join(uploadDir, fileName);
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    
    await writeFile(filePath, buffer);

    // Return file URL
    const fileUrl = `/uploads/${uploadType}/${fileName}`;
    const fullUrl = `${process.env.NEXT_PUBLIC_FRONTEND_URL || 'http://localhost:3000'}${fileUrl}`;

    return NextResponse.json({
      success: true,
      message: 'File uploaded successfully',
      fileName: fileName,
      originalName: file.name,
      fileUrl: fileUrl,
      fullUrl: fullUrl,
      fileSize: file.size,
      uploadType: uploadType
    });

  } catch (error) {
    console.error('Upload error:', error);
    return NextResponse.json(
      { error: 'Failed to upload file' },
      { status: 500 }
    );
  }
}

// Handle GET request to list uploaded files (optional)
export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type') || 'general';
    
    // This would list files in the upload directory
    // Implementation depends on your needs
    
    return NextResponse.json({
      message: `Files of type: ${type}`,
      // Could return list of files here
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to list files' },
      { status: 500 }
    );
  }
}
