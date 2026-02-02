import {
  LayoutDashboard,
  PenLine,
  History,
  BarChart2,
  Rss,
  Settings,
} from "lucide-react";

const menu = [
  { label: "Dashboard", icon: LayoutDashboard },
  { label: "Create", icon: PenLine, active: true },
  { label: "History", icon: History },
  { label: "Analytics", icon: BarChart2 },
  { label: "RSS Feeds", icon: Rss },
  { label: "Settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-[#020617] border-r border-slate-800 flex flex-col justify-between">
      {/* Logo */}
      <div>
        <div className="flex items-center gap-2 p-6 text-cyan-400 text-xl font-bold">
          ⚡ NewsFlow
        </div>

        {/* Menu */}
        <nav className="px-3 space-y-1">
          {menu.map((item) => (
            <div
              key={item.label}
              className={`flex items-center gap-3 px-4 py-2 rounded-lg cursor-pointer
                ${
                  item.active
                    ? "bg-cyan-500/10 text-cyan-400"
                    : "text-slate-400 hover:bg-slate-800"
                }`}
            >
              <item.icon size={18} />
              <span>{item.label}</span>
            </div>
          ))}
        </nav>
      </div>

      {/* User */}
      <div className="p-4 border-t border-slate-800 text-slate-400">
        <div className="text-sm">admin</div>
        <div className="text-xs">admin@gmail.com</div>
      </div>
    </aside>
  );
}
