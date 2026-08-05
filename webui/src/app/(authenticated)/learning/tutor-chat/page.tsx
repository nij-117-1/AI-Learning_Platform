import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { TutorChatPage } from "@/features/learning/tutor-chat/components/pages/TutorChatPage";

export const metadata: Metadata = {
  title: "Tutor Chat | Learning",
  description: "A topic-scoped tutor chatbot that explains concepts and breaks them down each turn.",
};

export default function TutorChatRoutePage() {
  return (
    <>
      <SetPageTitle title="Tutor Chat" />
      <TutorChatPage />
    </>
  );
}
