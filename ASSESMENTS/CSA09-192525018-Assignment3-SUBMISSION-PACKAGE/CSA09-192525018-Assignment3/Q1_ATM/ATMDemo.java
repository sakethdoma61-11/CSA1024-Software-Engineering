import java.util.*;
class InvalidAmountException extends Exception { InvalidAmountException(String m){super(m);} }
class InsufficientFundsException extends Exception { InsufficientFundsException(String m){super(m);} }
public class ATMDemo {
 static int withdraw(String input, double balance) throws InvalidAmountException, InsufficientFundsException {
  int amount;
  try { amount=Integer.parseInt(input); }
  catch(NumberFormatException e){ throw new IllegalArgumentException("Amount must be a whole number",e); }
  if(amount<=0) throw new InvalidAmountException("Amount must be positive");
  if(amount>balance) throw new InsufficientFundsException("Insufficient balance");
  return (int)(balance-amount);
 }
 public static void main(String[] args){
  String[] tests={"200","abc","-10","900","50"}; double balance=500;
  for(String t:tests){ try { balance=withdraw(t,balance); System.out.println(t+" => SUCCESS; balance="+balance); }
   catch(IllegalArgumentException e){System.out.println(t+" => INPUT ERROR: "+e.getMessage());}
   catch(InvalidAmountException|InsufficientFundsException e){System.out.println(t+" => BUSINESS ERROR: "+e.getMessage());}
   finally {System.out.println("  finally executed");}
  }
 }
}
