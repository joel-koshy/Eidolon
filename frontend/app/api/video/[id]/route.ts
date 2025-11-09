import { NextResponse } from "next/server";
import { getVideoById } from "@/server/mongodb"; // adjust import path

export async function GET(req: Request, { params }: { params: { id: string } }) {
  try {
    const video = await getVideoById(params.id);

    if (!video) {
      return NextResponse.json({ error: "Video not found" }, { status: 404 });
    }

    return NextResponse.json(video, { status: 200 });
  } catch (error) {
    console.error("Error in getVideoById API:", error);
    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
  }
}
