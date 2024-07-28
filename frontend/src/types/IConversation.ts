export interface IConversation {
    id: number;
    user_id: number;
    model_name: string;
    timestamp: string;
    user_score: number,
    user_feedback: string;
    summary: string;
}