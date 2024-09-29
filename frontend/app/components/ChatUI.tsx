import { useState } from "react"
import { Chat } from "../models/Chat"
import { useForm } from "@mantine/form"
import { ChatLog } from "./ChatLog"
import { Button, TextInput } from "@mantine/core"


export interface ChatUIProps {
  initChats: Chat[],
  saveUserChat: (message: string) => Promise<Chat>,
  chatResponse: (message: string) => Promise<Chat>,
}

export default function ChatUI({ initChats, saveUserChat, chatResponse }: ChatUIProps) {

  const [allChats, setChat] = useState<Chat[]>(initChats)
  const appendChat = (chat: Chat) => setChat([...allChats, chat])

  type FormValues = { message: string, }
  const form = useForm<FormValues>()
  const formSubmit = async ({ message }: FormValues) => {
    await saveUserChat(message).then(appendChat)
    await chatResponse(message).then(appendChat)
  }

  return (
    <div>
      <ChatLog chats={allChats} />

      <form onSubmit={form.onSubmit(formSubmit)}>

      <TextInput 
        label="chat message" 
        placeholder="Type your message here!" 
        key={form.key('message')} 
        {...form.getInputProps('message')}
      />
      <Button type="submit" />
      </form>
    </div>
  )
}
