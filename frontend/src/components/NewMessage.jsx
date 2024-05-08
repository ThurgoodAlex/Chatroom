import { useApi, useAuth } from "../utils/hooks.js";
import Button from "../assets/Button";
import { useState } from "react";
import { QueryClient, useMutation, useQueryClient } from "react-query";
import { useNavigate, useParams } from "react-router-dom";


function Input(props){
    return(
        <div className="flex flex-col py-2">
            <label className="test-s text-gray-400" htmlFor="{props.name}">
            {props.name}
            </label>
            <input
            {...props}
            className="border rounded bg-transparent px-2 py-1"
            />
        </div>
    );
}

function Checkbox(props) {
    return (
      <div className="flex flex-row py-2">
        <input
          {...props}
          className="border rounded bg-transparent px-2 py-1"
          type="checkbox"
        />
        <label className="text-s text-gray-400 ml-4" htmlFor={props.name}>
          {props.name}
        </label>
      </div>
    );
  }

function NewMessageForm(){
    const queryClient = useQueryClient()
    const navigate = useNavigate()
    const { token } = useAuth()
    const api = useApi()

    const {chatId} = useParams()
    const [message, setMessage] = useState("")

    const mutation = useMutation({
        
        mutationFn: () =>(
            api.post(
                `/chats/${chatId}/messages`,
                {
                    chatId,
                    text: message
                },
            ).then((response) => response.json())
        ),
        onSuccess: (data) => {
            console.log(data)
            queryClient.invalidateQueries(["chats"]);
            navigate(`/chats/${data.message.chat_id}`);
          },
    });

    const onSubmit = (e) => {
        e.preventDefault();
        mutation.mutate();
        setMessage("");
    };
    return (
        <form onSubmit={onSubmit}>
          <Input
            name="message"
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <Button type="submit">submit</Button>
        </form>
      );

}
function NewMessage() {
    return (
      <div className="w-96">
        <h2 className="text-center text-2xl font-bold">add a new message</h2>
        <NewMessageForm />
      </div>
    );
  }
  
  export default NewMessage;
    