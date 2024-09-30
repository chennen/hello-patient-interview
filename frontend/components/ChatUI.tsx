'use client'

import { Chat } from "../models/Chat";
import { ChatLog } from "./ChatLog";
import { ChatThread, User } from "../models";
import { submitChat } from "../actions/chat";
import { useOptimistic } from "react";
import { DateTime } from "luxon";

export interface ChatUIProps {
  initChats: Chat[];
  user: User;
  thread: ChatThread;
}

export default function ChatUI({ initChats, user, thread }: ChatUIProps) {

  // shamelessly stolen from the useOptimistic hook doc page
  const formSubmit = async (data: FormData) => {

    const message = data.get('message') as string

    // stick a placeholder message in the list of chats
    addOptimisticChat({
      message,
      username: user.name,
      time: DateTime.now().toISO(),
    })

    await submitChat(message, thread.id, user.id)
  }

  const [optimisticChats, addOptimisticChat] = useOptimistic(
    initChats,
    (chats, newChat: Chat) => [...chats, newChat]
  )

  // use chatGPT to make text input and button look nice!
  return (
    <>
      <ChatLog chats={optimisticChats} />
      <form action={formSubmit} className="max-w-md mx-auto p-4">
        <textarea
          name="message"
          className="w-full p-2 mb-4 border border-gray-300 rounded-lg text-black focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
          placeholder="Type your message here..."
        />
        <button className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 shadow-md">
          Send Message
        </button>
      </form>
    </>
  );
}
