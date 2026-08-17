package com.novaagent.app.data.api

import retrofit2.http.*
import retrofit2.Response
import com.google.gson.annotations.SerializedName

// Request-Response schemas mapping backend
data class AuthRequest(
    @SerializedName("email") val email: String,
    @SerializedName("password") val password: String
)

data class AuthResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("token_type") val tokenType: String
)

data class ChatMessageRequest(
    @SerializedName("content") val content: String,
    @SerializedName("session_id") val sessionId: String
)

data class ChatMessageResponse(
    @SerializedName("response") val response: String,
    @SerializedName("session_id") val sessionId: String
)

data class TaskResponse(
    @SerializedName("id") val id: String,
    @SerializedName("title") val title: String,
    @SerializedName("description") val description: String?,
    @SerializedName("status") val status: String,
    @SerializedName("priority") val priority: String
)

data class NoteResponse(
    @SerializedName("id") val id: String,
    @SerializedName("title") val title: String,
    @SerializedName("content") val content: String
)

interface NovaApiService {
    // Auth Endpoints
    @POST("api/v1/auth/signup")
    async fun signup(@Body request: AuthRequest): Response<Unit>

    @POST("api/v1/auth/login")
    async fun login(@Body request: AuthRequest): Response<AuthResponse>

    // Chat Endpoints
    @POST("api/v1/chat/message")
    async fun sendChatMessage(@Body request: ChatMessageRequest): Response<ChatMessageResponse>

    // Notes Endpoints
    @GET("api/v1/notes")
    async fun getNotes(): Response<List<NoteResponse>>

    @POST("api/v1/notes")
    async fun createNote(@Body note: Map<String, String>): Response<NoteResponse>

    // Tasks Endpoints
    @GET("api/v1/tasks")
    async fun getTasks(): Response<List<TaskResponse>>

    @POST("api/v1/tasks")
    async fun createTask(@Body task: Map<String, String>): Response<TaskResponse>
}
