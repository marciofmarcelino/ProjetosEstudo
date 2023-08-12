import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;






public class servidor {

    
    private static ServerSocket server;


    public static void main(String[] args){
        try{
        servidor.start(3222);
        Socket clientsocket = servidor.esperaconexao();
        servidor.trataconexão(clientsocket);
        }
    catch (IOException e) {
        System.out.println("ocorreu um erro");

            }
    }



    

    // criar socket 

    public static void start (int PORT) throws IOException {
    server = new ServerSocket(PORT);
    System.out.println("Server criado porta :"+PORT);
}

    // espera a conexao
    public static Socket esperaconexao() throws IOException {
        System.out.println("Aguardando conexão .... ..  .. ");
        Socket clientsocket = server.accept();
        System.out.print("conexão aceita.");
        return clientsocket;

    }

    public static void trataconexão( Socket clientSocket) throws IOException
    {
        /* protocolo da aplicação
            streams de entrada e saida; 
            tratar o protocolo
        */
                    /*criar o objeto stream  */

        
           
            /*output que será enviado ao cliente,serializado, stream write */
            ObjectOutputStream output = new ObjectOutputStream(clientSocket.getOutputStream());

         /*input recebido do cliente, desserialização , stream lida */
            ObjectInputStream input = new ObjectInputStream(clientSocket.getInputStream());

            String msg = input.readUTF(); //msg recebida e armazenada
            System.out.println("mensagem recebida: "+msg);
            output.writeUTF("Hello Word!!"); //msg que sera enviada
            output.flush();
            System.out.println("mensagem enviada");

            input.close();
            output.close();
            server.close();

        

    }
    
    


}
