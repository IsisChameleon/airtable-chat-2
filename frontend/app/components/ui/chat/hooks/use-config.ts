"use client";

import { useEffect, useMemo, useState } from "react";

export interface ChatConfig {
  chatAPI?: string;
  starterQuestions?: string[];
}

export function useClientConfig() {
  const CONFIG_ENDPOINT_PATH = "/api/chat/config";
  const chatAPIOrigin = process.env.NEXT_PUBLIC_CHAT_API;
  const [config, setConfig] = useState<ChatConfig>({
    chatAPI: chatAPIOrigin,
  });

  const configEndpointRoute = useMemo(() => {
    const backendOrigin = chatAPIOrigin ? new URL(chatAPIOrigin).origin : "";
    return `${backendOrigin}${CONFIG_ENDPOINT_PATH}`;
  }, [chatAPIOrigin]);

  useEffect(() => {
    fetch(configEndpointRoute)
      .then((response) => response.json())
      .then((data) => setConfig({ ...data, chatAPI: chatAPIOrigin }))
      .catch((error) => console.error("Error fetching config", error));
  }, [chatAPIOrigin, configEndpointRoute]);

  return config;
}
