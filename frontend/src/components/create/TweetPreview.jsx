export default function TweetPreview({ content }) {
  if (!content) return null;

  return (
    <div className="bg-[#020617] border border-slate-700 p-5 rounded-xl text-white">
      <h3 className="font-semibold mb-2">Generated Tweet</h3>

      {content.imageUrl && (
        <img
          src={`http://localhost:5000/${content.imageUrl}`}
          alt="preview"
          className="rounded mb-3"
        />
      )}

      <p className="text-slate-200">{content.tweet}</p>
    </div>
  );
}
