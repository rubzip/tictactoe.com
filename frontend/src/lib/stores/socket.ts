import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';
import { authStore } from './auth';

export enum MessageType {
    MOVE = 'MOVE',
    GAME_STATE = 'GAME_STATE',
    CHAT = 'CHAT',
    ERROR = 'ERROR',
    JOIN = 'JOIN',
    LEAVE = 'LEAVE',
    QUEUE_JOIN = 'QUEUE_JOIN',
    QUEUE_LEAVE = 'QUEUE_LEAVE',
    MATCH_FOUND = 'MATCH_FOUND'
}

interface SocketMessage {
    type: MessageType;
    payload: any;
}

const WS_BASE = 'ws://localhost:8000/ws';

const createSocketStore = () => {
    const { subscribe, set, update } = writable<{
        connected: boolean;
        error: string | null;
    }>({
        connected: false,
        error: null
    });

    let socket: WebSocket | null = null;
    const handlers = new Set<(msg: SocketMessage) => void>();

    return {
        subscribe,
        connect: () => {
            if (!browser || socket) return;

            const token = get(authStore).token;
            const clientId = Math.random().toString(36).substring(7);
            const url = `${WS_BASE}/${clientId}${token ? `?token=${token}` : ''}`;

            socket = new WebSocket(url);

            socket.onopen = () => {
                update((s) => ({ ...s, connected: true, error: null }));
                console.log('WS Connected');
            };

            socket.onmessage = (event) => {
                const message: SocketMessage = JSON.parse(event.data);
                handlers.forEach((h) => h(message));
            };

            socket.onerror = () => {
                update((s) => ({ ...s, error: 'WebSocket error occurred' }));
            };

            socket.onclose = () => {
                update((s) => ({ ...s, connected: false }));
                socket = null;
                // Attempt reconnect after 3 seconds
                setTimeout(() => socketStore.connect(), 3000);
            };
        },
        send: (type: MessageType, payload: any) => {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type, payload }));
            }
        },
        onMessage: (handler: (msg: SocketMessage) => void) => {
            handlers.add(handler);
            return () => handlers.delete(handler);
        },
        disconnect: () => {
            if (socket) {
                socket.close();
                socket = null;
            }
        }
    };
};

export const socketStore = createSocketStore();
