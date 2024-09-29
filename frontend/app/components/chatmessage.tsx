
export interface ChatMessageProps {
  sender: string,
  text: string,
}

export const ChatMessage = ({sender, text}: ChatMessageProps) => ( <p>{sender}: {text}</p> )

