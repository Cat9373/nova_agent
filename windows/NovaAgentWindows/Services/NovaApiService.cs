using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace NovaAgentWindows.Services
{
    public class NovaApiService
    {
        private readonly HttpClient _httpClient;
        private string? _token;

        public NovaApiService(string baseUrl = "http://localhost:8000")
        {
            _httpClient = new HttpClient { BaseAddress = new Uri(baseUrl) };
            _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        }

        public void SetToken(string token)
        {
            _token = token;
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        }

        public async Task<string> SendChatMessageAsync(string content, string sessionId)
        {
            var payload = new
            {
                content = content,
                session_id = sessionId
            };

            var json = JsonConvert.SerializeObject(payload);
            var httpContent = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync("api/v1/chat/message", httpContent);
            response.EnsureSuccessStatusCode();

            var responseJson = await response.Content.ReadAsStringAsync();
            dynamic result = JsonConvert.DeserializeObject(responseJson) ?? throw new InvalidOperationException();
            return result.response;
        }

        public async Task<string> GetNotesAsync()
        {
            var response = await _httpClient.GetAsync("api/v1/notes");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<string> GetTasksAsync()
        {
            var response = await _httpClient.GetAsync("api/v1/tasks");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
    }
}
// Windows Service integration blueprint
