import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ sessionId: string }> }
) {
  try {
    const { sessionId } = await params;

    // TODO: Replace with actual backend API call
    // This should poll your backend for the video generation status
    
    // Example backend integration:
    // const response = await fetch(
    //   `${process.env.BACKEND_URL}/api/video-status/${sessionId}`
    // );
    // const data = await response.json();
    // return NextResponse.json(data);

    // Mock response for development
    // Simulate video generation completing after 10 seconds
    const sessionTimestamp = parseInt(sessionId.split('_')[1] || '0');
    const elapsed = Date.now() - sessionTimestamp;

    if (elapsed < 10000) {
      // Still generating
      return NextResponse.json({
        status: 'generating',
        progress: Math.min(Math.floor((elapsed / 10000) * 100), 99),
        message: 'Generating Manim animation...',
      });
    } else {
      // Completed - return mock video URL
      return NextResponse.json({
        status: 'completed',
        videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
        message: 'Video generated successfully',
      });
    }
  } catch (error) {
    console.error('Error in video-status:', error);
    return NextResponse.json(
      { status: 'error', error: 'Failed to get video status' },
      { status: 500 }
    );
  }
}
