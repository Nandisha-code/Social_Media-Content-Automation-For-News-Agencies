export default function Header({ title, subtitle }) {
  return (
    <header className="mb-6">
      <h1 className="text-2xl font-semibold text-white">
        {title} <span className="text-cyan-400">{subtitle}</span>
      </h1>
      <p className="text-slate-400 mt-1">
        {subtitle}
      </p>
    </header>
  );
}