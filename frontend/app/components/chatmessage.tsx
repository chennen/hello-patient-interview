
export interface Props {
  isCurrentUser: boolean,
  sender: string,
  text: string,
}
export const chatmessage = ({sender, text}: Props) => ( <p>{sender}: {text}</p> )

