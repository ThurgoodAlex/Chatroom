import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import NewMessage from "./NewMessage"
import { useApi } from "../utils/hooks";

const chatpreview = [
  "flex flex-col flex-grow bg-gray-800 p-2 mb-2 items-center h-full border-2 border-solid border-blue-500 bg-slate-700 p-2.5 mb-2.5 hover:text-white hover:bg-neutral-700" 
]

const messagecard = [
  "flex flex-col h-96 border-2 border-solid border-green-300 overflow-y-scroll p-2.5 rounded-md"
]

function ChatPreview({ chat }) {
  return (

    <Link className={chatpreview} to={`/chats/${chat.id}`}>
      <div className="font-bold">{chat.name}</div>
    </Link>
  );
}

function ChatMessages() {
  const { chatId } = useParams();
  const api = useApi();

  const navigate = useNavigate();
  const { data, isLoading } = useQuery({
    queryKey: ["chats", chatId],
    queryFn: () => {
      if (!chatId) {
        return undefined
      }
      return api.get(`/chats/${chatId}/messages`)
      
        .then((response) => {

          if (!response.ok) {
            response.status === 404 ?
              navigate("/error/404") :
              navigate("/error");
          }
          return response.json()
        })
    },
  });

  if (isLoading || !chatId) {
    return (
    <div className="pr-7 font-bold">
      <Instructions chat={{}} />
    </div>
    
    );
  }

  if (data?.messages) {
    return <MessageCard messages={data.messages} />;
  }

  return <Navigate to="/error" />;
}

function MessageCard({ messages }) {
  // console.log(messages);

  return (
    <div className="h-full">
      <div className={messagecard}>
        {messages.map((message, index) => (
          <div className ="border-2 border-solid border-rose-300 rounded-lg"key={index}>
            <h2 className="font-bold pl-2.5">{message.user.username || "Name"}</h2>
              <div className="text-s pl-2.5">{message.text}</div>
              <div className="text-xs pt-2.5 pl-2.5">{new Date(message.created_at).toLocaleString('en-US', { weekday: 'short', month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit' })}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Instructions() {

  return ( 
      <h2>Please Select A Chat</h2>
  );
}

function EmptyChatList() {
  return <ChatList chats={[0, 1, 2, 3, 4].map((index) => ({
    name: "loading...",
    id: index
  }))} />
}

function ChatList({ chats }) {
  // console.log(chats);
  return (
    <div className="flex flex-col h-full pl-2.5">
      {chats.map((chat) => (<ChatPreview key={chat.id} chat={chat} />
      ))}
    </div>
  );
}


function ChatsPage() {
  const api = useApi()
  const navigate = useNavigate();
  const { data, isLoading, error } = useQuery({
    queryKey: ["chats"],
    queryFn: () => (
      // fetch('http://127.0.0.1:8000/chats')
      api.get(`/chats`)
        .then((response) => {
          if (!response.ok) {
            response.status === 404 ?
              navigate("/error/404") :
              navigate("/error");
          }
          return response.json()

        })
    ),
  });

  if (error) {
    return <Navigate to="/error" />
  }

  return (
    <>
      <div className="pb-2.5 pl-2.5 font-bold">
        <h1>Chats</h1>
      </div>
      <div className="flex flex-row justify-between h-3/4 gap-12">
        {!isLoading && data?.chats ? (
          <>
            <ChatList chats={data.chats} />
            <div className="flex items-center justify-center flex-grow">
              <div className="flex flex-col p-2.5">
                <ChatMessages />
                <div className="pt-2.5">
                  <Message />
                </div>
              </div>
            </div>
          </>
        ) : (
          <EmptyChatList />
        )}
      </div>
    </>
  );
}


function Message(){
  const {chatId} = useParams();

  if (chatId) {
    return (
      <NewMessage chatId={chatId} />
    );
  }


}





export default ChatsPage