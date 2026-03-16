"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

export default function NavBar() {
  const pathname = usePathname();
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/logout", { method: "POST" });
    router.push("/login");
  }

  const linkClass = (href: string) =>
    `px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
      pathname === href
        ? "bg-[#1a5c6b] text-white"
        : "text-[#555550] hover:bg-[#e8f0f4] hover:text-[#1a5c6b]"
    }`;

  return (
    <nav className="bg-white border-b border-[#e5e5e0] px-6 py-3 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center gap-6">
        <div className="bg-[#111] text-white font-extrabold text-sm px-3 py-1.5 rounded-md tracking-tight">
          lower<span className="text-[#4fc3f7]">.com</span>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/presentation" className={linkClass("/presentation")}>
            Presentation
          </Link>
          <Link
            href="/supporting-queries"
            className={linkClass("/supporting-queries")}
          >
            Supporting Queries
          </Link>
        </div>
      </div>
      <button
        onClick={handleLogout}
        className="text-sm text-[#8a8a82] hover:text-[#c0392b] transition-colors cursor-pointer"
      >
        Logout
      </button>
    </nav>
  );
}
