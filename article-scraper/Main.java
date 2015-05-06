import java.net.URL;
import de.l3s.boilerpipe.extractors.ArticleExtractor;


public class Main
{
	public static void main(String [] arr) 
	{
		try
		{
			URL url = new URL(arr[0]);
			String text = ArticleExtractor.INSTANCE.getText(url);
			System.out.println(text);
		}
		catch(Exception e)
		{
			System.out.println("NO CONTENT");
		}
	}
}
