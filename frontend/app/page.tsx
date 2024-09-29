import { User, ChatThread, Chat, ChatbotUser} from './models'
import { ChatUI } from './components'
import { DateTime } from 'luxon'
import { GetServerSideProps, InferGetServerSidePropsType } from 'next';

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default async function Home() {

  const user: User = await fetch(`${apiUrl}/users/me`).then(r => r.json())
  const thread: ChatThread = await fetch(`${apiUrl}/chats/me`).then(r => r.json())
  const initChats: Chat[] = await fetch(`${apiUrl}/chats/me/messages`).then(r => r.json())

  const threadId = thread.id
  const makeNewChat = (user: User) => (message: string): Chat => ({
    threadId,
    username: user.name,
    message,
    time: DateTime.now().toUTC().toISO()
  })
  const makeChatbotChat = makeNewChat(ChatbotUser)
  const makeUserChat = makeNewChat(user)

 // TODO: this is an API call, it should generate + save the chat before responding
  const getBotReply = (message: string) =>
  fetch(
      `${apiUrl}/chats/bot/prompt`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ message }),
      }
    )
    .then(res => res.text())
    .then(makeChatbotChat)

  const saveUserChat = async (message: string) => {
    const newChat = makeUserChat(message)
    await fetch(
      `${apiUrl}/chats/me/messages`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(newChat),
      }
    )
    return newChat
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      Hello, {user.name}! 

      <ChatUI initChats={initChats} user={user} saveUserChat={saveUserChat} chatResponse={getBotReply}/>

    </main>
  );
}
