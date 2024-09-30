import { Chat } from "../models/Chat";
import { ChatMessage } from "./ChatMessage";

export interface ChatLogProps {
  chats: Chat[];
}

export const ChatLog = ({ chats }: ChatLogProps) => (
  <div>
    {chats.map((c) => (
      <ChatMessage username={c.username} message={c.message} key={c.time} />
    ))}
  </div>
);
