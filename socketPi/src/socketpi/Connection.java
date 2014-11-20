/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package socketpi;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author luisponcedeleon
 */
public class Connection implements Runnable {
    
    private static Connection INSTANCE;

    FrameMain frame;
    
    ServerSocket socket;
    Socket c;
    
    BufferedReader input;
    DataOutputStream output;
    
    String lastInputString;
    
    private Connection(){
        
    }
    
    public static Connection getInstance(){
        if(INSTANCE==null){
            INSTANCE = new Connection();
        }
        return INSTANCE;
    }

    public void Init(FrameMain f){
        frame = f;
        try {
            socket = new ServerSocket(8083);
            
            c = socket.accept();
            
            input = new BufferedReader
                            (new InputStreamReader(c.getInputStream()));
            
            output = new DataOutputStream(c.getOutputStream());

            
            
        } catch (IOException ex) {
            Logger.getLogger(Connection.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    @Override
    public void run() {
        for(;;){
            execute();
            
            
        }
    }

    private void execute() {
        try {
            input = new BufferedReader
                            (new InputStreamReader(c.getInputStream()));
            
            output = new DataOutputStream(c.getOutputStream());
            
            if (input.ready()) {
                String newInput = input.readLine();
                if(!newInput.equals(lastInputString)){
                    lastInputString=newInput;
                    System.out.println(newInput);
                    frame.setPos(newInput);
                    
                }
            }
            
        } catch (IOException ex) {
            Logger.getLogger(Connection.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    public void write(String pos) throws IOException{
        byte[] utf8 = pos.getBytes("UTF-8");
            
        output.write(utf8);
    }
}
