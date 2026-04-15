import { writable } from 'svelte/store';
import { socketStore, MessageType } from './socket';

export interface GameState {
    board: string[][];
    turn: 'X' | 'O';
    status: 'KEEP_PLAYING' | 'X_WINS' | 'O_WINS' | 'DRAW';
    win_line: number[][] | null;
    player_usernames: { X?: string; O?: string };
    ai_difficulties: { X?: string | null; O?: string | null };
}

interface ChatMessage {
    username: string;
    message: string;
    client_id?: string;
}

interface GameStore {
    state: GameState | null;
    chat: ChatMessage[];
    matchmaking: {
        searching: boolean;
        matchFound: boolean;
    };
    error: string | null;
    role: 'X' | 'O' | 'SPECTATOR' | null;
    room_id: string | null; // Added to track room before full state is ready
}

const createGameStore = () => {
    const { subscribe, set, update } = writable<GameStore>({
        state: null,
        chat: [],
        matchmaking: {
            searching: false,
            matchFound: false
        },
        error: null,
        role: null,
        room_id: null
    });

    // Register listener for socket messages
    socketStore.onMessage((msg) => {
        switch (msg.type) {
            case MessageType.GAME_STATE:
                update((s) => ({ ...s, state: msg.payload }));
                break;
            case MessageType.CHAT:
                update((s) => ({ ...s, chat: [...s.chat, msg.payload] }));
                break;
            case MessageType.MATCH_FOUND:
                update((s) => ({
                    ...s,
                    room_id: msg.payload.room_id,
                    matchmaking: { searching: false, matchFound: true }
                }));
                break;
            case MessageType.JOIN:
                if (msg.payload.status === 'success') {
                    update((s) => ({
                        ...s,
                        state: msg.payload.game_state,
                        role: msg.payload.role,
                        room_id: msg.payload.room_id || s.room_id
                    }));
                }
                break;
            case MessageType.ERROR:
                update((s) => ({ ...s, error: msg.payload }));
                break;
            case MessageType.QUEUE_JOIN:
                update((s) => ({
                    ...s,
                    matchmaking: { ...s.matchmaking, searching: true }
                }));
                break;
            case MessageType.QUEUE_LEAVE:
                update((s) => ({
                    ...s,
                    matchmaking: { ...s.matchmaking, searching: false }
                }));
                break;
        }
    });

    return {
        subscribe,
        joinQueue: () => socketStore.send(MessageType.QUEUE_JOIN, {}),
        leaveQueue: () => socketStore.send(MessageType.QUEUE_LEAVE, {}),
        makeMove: (row: number, col: number) =>
            socketStore.send(MessageType.MOVE, { row, col }),
        sendMessage: (message: string) =>
            socketStore.send(MessageType.CHAT, { message }),
        joinRoom: (room_id: string) =>
            socketStore.send(MessageType.JOIN, { room_id }),
        consumeMatch: () =>
            update((s) => ({
                ...s,
                room_id: null,
                matchmaking: { searching: false, matchFound: false }
            })),
        reset: () =>
            set({
                state: null,
                chat: [],
                matchmaking: { searching: false, matchFound: false },
                error: null,
                role: null,
                room_id: null
            })
    };
};

export const gameStore = createGameStore();
