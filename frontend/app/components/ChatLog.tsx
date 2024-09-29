import { ScrollArea } from '@mantine/core'
import { Chat } from '../models/Chat'

export interface ChatLogProps {
  chats: Chat[],
}

export const ChatLog = ({ chats }: ChatLogProps) => {

  return (
    <ScrollArea>
      <div>

      </div>
    </ScrollArea>
  )
}
