import { NextRequest, NextResponse } from "next/server";
import { createHash } from "crypto";

const TOKEN_VALUE = createHash("sha256")
  .update("authenticated")
  .digest("hex");

export async function POST(request: NextRequest) {
  const { password } = await request.json();

  if (password === process.env.SITE_PASSWORD) {
    const response = NextResponse.json({ success: true });
    response.cookies.set("auth-token", TOKEN_VALUE, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60 * 24 * 7, // 7 days
    });
    return response;
  }

  return NextResponse.json({ error: "Invalid password" }, { status: 401 });
}
