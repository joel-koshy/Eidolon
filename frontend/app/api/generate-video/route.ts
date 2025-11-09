import { NextResponse } from "next/server";
import { createVideoPrompt } from "@/server/mongodb";

export const dynamic = "force-dynamic"; 

type GenerateVideoInput = {
  userid: string;
  prompt: string;
};

export async function POST(req: Request) {
  try {
    console.log("Received request to /api/createVideoPrompt");
    console.log("Request body:", req.body);
    const body: GenerateVideoInput = await req.json();
    // Optional: basic validation
    if (!body.userid || !body.prompt) {
      return NextResponse.json(
        { success: false, error: "Missing userid or prompt" },
        { status: 400 }
      );
    }

    const result = await createVideoPrompt(body);

    if (result.success) {
        // @ts-ignore
      console.log("Inserted ID:", result.data.insertedId); // print to server log
      return NextResponse.json(
        // @ts-ignore
        { success: true, insertedId: result.data.insertedId },
        { status: 200 }
      );
    } else {
      return NextResponse.json(
        { success: false, error: "Failed to create video prompt" },
        { status: 500 }
      );
    }
  } catch (e: any) {
    console.error("Error in createVideoPrompt:", e);
    return NextResponse.json(
      { success: false, error: e.message || "Unknown error" },
      { status: 500 }
    );
  }
}
