"use server";

const timeout = (ms: number) => new Promise((res) => setTimeout(res, ms));

import { revalidatePath } from "next/cache";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export async function submitChat(
  message: string,
  threadId: string,
  userId: string,
) {
  // user chat
  await fetch(`${apiUrl}/threads/default/chats`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      message,
      thread_id: threadId,
      user_id: userId,
    }),
  }).then((res) => res.text());

  // bot response
  await fetch(`${apiUrl}/threads/default/bot-chat`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ message, thread_id: threadId }),
  }).then((res) => res.text());

  // simulate slow chatbot response
  await timeout(2000);

  // ASSUMPTION: refresh => refetch the data when form submits
  revalidatePath("/");
}
