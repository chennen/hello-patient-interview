import { User, ChatThread, Chat, ChatbotUser } from "../models";
import ChatUI from "../components/ChatUI";

// hint to NextJS that this page is not static - need to fetch data on each refresh
export const revalidate = 0


const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default async function Home() {
  // pre-fetch data for the page from backend API
  const [user, thread, initChats] = await Promise.all([
    fetch(`${apiUrl}/users/me`).then(r => r.json() as Promise<User>),
    fetch(`${apiUrl}/users/me/threads/default`).then(r => r.json() as Promise<ChatThread>),
    fetch(`${apiUrl}/threads/default/chats`).then(r => r.json() as Promise<Chat[]>),
  ]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      Hello, {user.name}!
      <ChatUI initChats={initChats} user={user} thread={thread} />
    </main>
  );
}
