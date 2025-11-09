import { NextResponse } from "next/server";
import { getLatestPendingVideos } from "@/server/mongodb";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const result = await getLatestPendingVideos(10);

    if (result.success) {
      return NextResponse.json({ success: true, data: result.data }, { status: 200 });
    } else {
      return NextResponse.json({ success: false, error: result.error }, { status: 500 });
    }
  } catch (e: any) {
    console.error("Error in getLatestPendingVideos:", e);
    return NextResponse.json({ success: false, error: e.message || "Unknown error" }, { status: 500 });
  }
}
