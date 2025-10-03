#!/usr/bin/env python3
"""
Simple WebSocket server for sending messages to the app
Usage: python websocket_server.py
"""

import asyncio
import websockets
import json
import time
import random

# List of demo messages to send
DEMO_MESSAGES = [
    {
        "from": "Ministerie van EZK",
        "subject": "Nieuwe regeling MKB innovatie",
        "content": "Een nieuwe regeling voor MKB innovatie is nu beschikbaar. Subsidie tot €50.000 voor innovatieve projecten."
    },
    {
        "from": "Gemeente Amsterdam", 
        "subject": "Circulaire economie subsidie",
        "content": "Subsidie beschikbaar voor projecten die bijdragen aan de circulaire economie. Aanvragen mogelijk tot 31 maart."
    },
    {
        "from": "RVO Nederland",
        "subject": "Energie-investeringsaftrek",
        "content": "Nieuwe mogelijkheden voor energie-investeringsaftrek. Uw project kan in aanmerking komen voor 45% aftrek."
    },
    {
        "from": "Provincie Zuid-Holland",
        "subject": "Warmtenet project Den Haag",
        "content": "Er wordt gezocht naar partners voor het warmtenet project in Den Haag. Uw bedrijf kan mogelijk deelnemen."
    }
]

connected_clients = set()

async def register_client(websocket, path):
    """Register a new client"""
    connected_clients.add(websocket)
    print(f"📱 Nieuwe client verbonden. Totaal: {len(connected_clients)}")
    
    try:
        await websocket.wait_closed()
    except:
        pass
    finally:
        connected_clients.remove(websocket)
        print(f"📱 Client afgesloten. Totaal: {len(connected_clients)}")

async def send_periodic_messages():
    """Send periodic demo messages to all connected clients"""
    while True:
        if connected_clients:
            # Select random message
            message = random.choice(DEMO_MESSAGES).copy()
            message["time"] = time.strftime("%H:%M")
            message["id"] = f"msg_{int(time.time())}"
            
            # Send to all clients
            message_json = json.dumps(message)
            disconnected = []
            
            for client in connected_clients:
                try:
                    await client.send(message_json)
                    print(f"📧 Bericht verzonden: {message['subject']}")
                except:
                    disconnected.append(client)
            
            # Remove disconnected clients
            for client in disconnected:
                connected_clients.discard(client)
        
        # Wait 30-60 seconds before sending next message
        await asyncio.sleep(random.randint(30, 60))

async def main():
    print("🚀 WebSocket Message Server gestart op ws://localhost:8765")
    print("📡 Wachtend op clients...")
    print("📨 Demo berichten worden elke 30-60 seconden verzonden")
    print("🛑 Druk Ctrl+C om te stoppen")
    
    # Start the periodic message sender
    message_task = asyncio.create_task(send_periodic_messages())
    
    # Start the WebSocket server
    async with websockets.serve(register_client, "localhost", 8765):
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("\n🛑 Server wordt gestopt...")
            message_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 WebSocket server gestopt")