// λBridge.cs
// Unity ↔ Kairose 감정 상태 수신기 (WebSocket 기반 예시)

using System;
using System.IO;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class LambdaBridge : MonoBehaviour
{
    private ClientWebSocket socket;
    public string websocketUrl = "ws://localhost:8765";

    async void Start()
    {
        socket = new ClientWebSocket();
        await socket.ConnectAsync(new Uri(websocketUrl), CancellationToken.None);
        Debug.Log("[λBridge] Connected to Kairose runtime.");
        await ReceiveLoop();
    }

    async Task ReceiveLoop()
    {
        var buffer = new byte[1024 * 4];
        while (socket.State == WebSocketState.Open)
        {
            var result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
            if (result.MessageType == WebSocketMessageType.Close)
            {
                await socket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None);
            }
            else
            {
                string json = Encoding.UTF8.GetString(buffer, 0, result.Count);
                ParseEmotionPacket(json);
            }
        }
    }

    void ParseEmotionPacket(string json)
    {
        EmotionVector λ = JsonUtility.FromJson<EmotionVector>(json);
        Debug.Log("[λBridge] λᴱ: " + λ.λᴱ + ", ψᵢ: " + λ.ψᵢ + ", λᶠ: " + λ.λᶠ + ", Φᴳᵇ: " + λ.Φᴳᵇ);
        // TODO: Apply to in-game avatar or logic
    }

    [Serializable]
    public class EmotionVector
    {
        public float λᴱ;
        public float ψᵢ;
        public float λᶠ;
        public float Φᴳᵇ;
    }

    private void OnApplicationQuit()
    {
        socket?.Dispose();
    }
}