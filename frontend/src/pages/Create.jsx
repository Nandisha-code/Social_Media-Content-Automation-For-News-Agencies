import { useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import Header from "../components/layout/Header";
import CreateTweetForm from "../components/create/CreateTweetForm";
import TweetPreview from "../components/create/TweetPreview";

export default function Create() {
  const [generated, setGenerated] = useState(null);

  return (
    <AppLayout>
      <Header
        title="Create"
        subtitle="Upload content and let AI generate engaging tweets for you"
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CreateTweetForm onGenerated={setGenerated} />
        <TweetPreview content={generated} />
      </div>
    </AppLayout>
  );
}
