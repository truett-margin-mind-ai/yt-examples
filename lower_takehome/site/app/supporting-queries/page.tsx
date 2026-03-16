import fs from "fs";
import path from "path";
import NavBar from "../components/NavBar";
import MarkdownContent from "./MarkdownContent";

export default function SupportingQueriesPage() {
  const mdPath = path.join(process.cwd(), "content", "supporting-queries.md");
  const content = fs.readFileSync(mdPath, "utf-8");

  return (
    <div className="min-h-screen bg-[#f7f7f5]">
      <NavBar />
      <div className="max-w-4xl mx-auto px-6 py-10">
        <MarkdownContent content={content} />
      </div>
    </div>
  );
}
