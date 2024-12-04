import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
  try {
    // const outputDir = path.join(
    //   process.cwd(),
    //   "..",
    //   "python-assessment",
    //   "output"
    // );
    const outputDir = path.join(process.cwd(), "src", "output");
    console.log("outputDir", outputDir);

    const products = [];

    // Read all JSON files in the output directory
    const files = fs.readdirSync(outputDir);
    for (const file of files) {
      if (file.endsWith(".json")) {
        const filePath = path.join(outputDir, file);
        const fileContent = fs.readFileSync(filePath, "utf-8");
        const fileProducts = JSON.parse(fileContent);
        products.push(...fileProducts);
      }
    }

    return NextResponse.json(products);
  } catch (error) {
    console.error("Error reading product data:", error);
    return NextResponse.json(
      { error: "Failed to fetch products" },
      { status: 500 }
    );
  }
}
