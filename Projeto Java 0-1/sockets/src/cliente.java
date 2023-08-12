import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;

public class cliente {
   
    public static void main(String[] args) throws IOException {
        try {
        // criar um socket 
         Socket socket = new Socket("localhost",3222);

        // inputs e outputs
        
       
        
        ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
        ObjectInputStream inp = new ObjectInputStream(socket.getInputStream());

        String msg = "hello";
        out.writeUTF(msg);
        
        out.flush();

        msg = inp.readUTF();
        System.out.println("Resposta: "+msg);

        out.close();
        inp.close();
        socket.close();

        }
        catch (IOException ex)
        {

        }  
        
        

    }
}
