# HTTP communication demo

This is a demo of a very simple messaging app to illustrate different types of browser-server communication.

The server uses python, use `./build.sh` to build the Docker image, then use `./run.sh python app.py` to run the server.

Look at `src/app.py` for server side details, basically it has the following endpoints:

/add_message - takes a `message` parameter, adds a message to the db
/messages - retrieves all messages on the server
/stream - server side push streaming endpoint
/ws - websocket endpoint


After running the server, the various examples are as follows:

http://localhost:5000/example1.html - basic webpage
http://localhost:5000/example2.html - Webpage with client side whole page refersh
http://localhost:5000/example3.html - AJAX
http://localhost:5000/example4.html - Server side push 
http://localhost:5000/example5.html - Websocket


# Lesson

## Basic HTTP

HTTP stands for Hypertext Transfer Protocol.  For the purpose of this lesson,
let's focus on the word "Protocol", which simply means a method of communication
between 2 parties.

HTTP was created in 1991 [https://tools.ietf.org/html/rfc1945](https://tools.ietf.org/html/rfc1945)
to facilitate the transfers of simply web pages between web browsers and web servers.  It was
designed to give scientists an easy way to share information.  Back in those days,
web pages mostly consist of text and small images.

The basic idea is as follows:

![Sequence diagram of HTTP communication](http.png)

A couple of important notes:

 * The server has no interest in identifying or remembering who made the request
 * This entire sequence happens for every webpage, even if it comes from the same browser
 * Once the browser receives the data (text and images) from the server, we assume that the users will take
 their time reading the content and won't make another request for a while

## Fast food restaurant analogy

An analogy can be made using you favoriate drive-thru restartuant.

 1. As a customer, you drive up to the kiosk
 2. You request food from the server
 3. The server receives your request
 4. The server goes to the kitchen to get your food
 5. The server returns food to you
 6. You drive away, enjoy your food

Just like in HTTP, if you need more food, you have to repeat the entire sequence.
The resturant does not care to identify or remember who you are.

## A basic webpage

 * [https://www.fsf.org/](https://www.fsf.org/) is an example of a basic webpage
 * If you open the "Developer tools" and then go to the "Network" tab, you can see the transfers of
 various text and image files

## Modern web

Since 1996, users have discovered that the web is an extrememly powerful communication medium,
and developers started pushing the limits of http based technologies.  Take Twitter for example,
it is a website that allows users to post and receive messages from each other.

## Example Application

To explore how the modern web works, I have created an example application that allows users to post
short anonymous messages.  To make things more interesting, random messages from twitter is injected
every 1-10 seconds.

### Classic HTTP

Let's start by looking at [http://localhost:5000/example1.html](http://localhost:5000/example1.html).

 * This example follows basic HTTP -- meaning that once the page finished loading, the connection
 between browser and server is no longer active
 * The problem here is that even if there new messages, the browser will not update
 * The only way to get the latest message is to "refresh"

### Auto refresh

To create a better user experience, developers tried different techniques.  One way
is to automate the referesh, like this:  [http://localhost:5000/example2.html](http://localhost:5000/example2.html)

But as you can see, the user experience is terrible, as the browser is constantly refreshing.

### AJAX

A better solution called AJAX (Asynchronous Javascript And XML) was crafted to combat the refersh problem.
It works by extending the capabilities of Javascript, essentailly allowing
Javascript to update the data and change the HTML elements in the background, without
refreshing the entire page.  You can see the result in
[http://localhost:5000/example3.html](http://localhost:5000/example3.html)

Noticed that there are no more refresh of the entire page.  If you look under the "Network" tab,
you can see that we are requesting data from the server every second.


What are to pros and cons of the AJAX approach?

Pros

 * Vastly improved user experience
 * Uses the same computing model as classic HTTP

Cons

 * Lots of requests made to the server, especially if the update is frequent
 * Not a solution to "real-time" systems

### Server Push (Server events)

AJAX is great when you don't need information to be "real-time".  But if you want to always
see the latest message being posted, constantly requesting new updates from client to server
is not efficient.

[http://localhost:5000/example4.html](http://localhost:5000/example4.html) uses an alternative
approach.  Check out the "Network" tab and you'll noticed that we no longer issue requests
to the server every x seconds.  Rather, we keep a "stream" open so we can receive updates
from the server constantly.

Like the AJAX example, message area is being refershed by Javascript, so users don't see
the refersh.  However, we are no longer following classic HTTP as we have a constant
connection opened to the server and is now getting real time updates.  You can actually
see the stream by visiting [http://localhost:5000/stream](http://localhost:5000/stream)

### Websocket

The server push example is great if you only want to receive messages, as the stream is
read-only.  You will notice that sending a message requires a separate connection to be made.

If we want truly efficient bi-directional communication, we need to completely break away
from the classic HTTP approach and allow one connection to be used for both sending and receiving
data.  This approach is called websocket: [http://localhost:5000/example5.html](http://localhost:5000/example5.html)

Take a look at the "Network" tab and you'll noticed that both sending and receiving of messages
will not produce additional network connections.  If you click on the "ws" item, you will
also noticed that the status code is "101 Switching Protocols", signifying that we
are moving completely away from the classic HTTP way of doing things.

## Conclusion

This concludes our overview of browser-server communication.  Below are some follow up questions:

 1. If websocket is so modern and efficient, why are we not using websocket everywhere?
 1. It seems like websocket can also be used to read a stream of data, why is "server send event" necessary?
 1. Besides text messaging, what other systems require "real-time" delivery of data?
 1. In both example 4 and example 5, we only get the new messages via the stream, whereas in example 3, we are getting
 all the historical messages from the server.  Modify examples 4 and 5 so a list of historical messages are also displayed.




