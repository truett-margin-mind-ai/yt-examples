import NavBar from "../components/NavBar";

export default function PresentationPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#f7f7f5]">
      <NavBar />
      <iframe
        src="/api/presentation"
        className="flex-1 w-full border-0"
        title="Lower Consumer Contact Strategy Analysis"
      />
    </div>
  );
}
