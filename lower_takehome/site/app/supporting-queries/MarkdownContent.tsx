"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github.css";

export default function MarkdownContent({ content }: { content: string }) {
  return (
    <article className="prose prose-zinc max-w-none prose-headings:font-bold prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg prose-pre:bg-[#1a1a1a] prose-pre:text-sm prose-table:text-sm prose-th:bg-[#f0f0ec] prose-th:px-3 prose-th:py-2 prose-td:px-3 prose-td:py-2 prose-td:border-[#e5e5e0] prose-th:border-[#e5e5e0] prose-hr:border-[#e5e5e0]">
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
        {content}
      </ReactMarkdown>
    </article>
  );
}
