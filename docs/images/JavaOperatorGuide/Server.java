package serverConnections;

import java.util.UUID;

public class Server {
	String username, password;
	
	public void initialize(String userName, String passWord) throws Exception{
		username = userName;
		password = passWord;
	}
	
	public String getData() throws Exception {
		return UUID.randomUUID().toString();
	}
	
	public void sendData(String message) throws Exception {
		System.out.println("Sinking server message: " + message);
	}
	
	void disconnect() throws RuntimeException{
		
	}
}