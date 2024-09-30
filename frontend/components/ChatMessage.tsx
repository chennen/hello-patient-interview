export interface ChatMessageProps {
  username: string;
  message: string;
}

export const ChatMessage = ({ username, message }: ChatMessageProps) => (
  <p>
    <b>{username}:</b> {message}
  </p>
);
