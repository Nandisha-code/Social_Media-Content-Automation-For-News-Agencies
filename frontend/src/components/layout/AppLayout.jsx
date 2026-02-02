import Sidebar from "./Sidebar";
import Footer from "./Footer";

export default function AppLayout({ children }) {
  return (
    <div className="flex min-h-screen bg-[#020617] text-white">
      <Sidebar />

      <main className="flex-1 px-8 py-6">
        {children}
        <Footer />
      </main>
    </div>
  );
}
