import { useMutation } from "@tanstack/react-query";
import { generateContentApi } from "../api/content.api";

export const useGenerateContent = () => {
  return useMutation({
    mutationFn: generateContentApi,
  });
};
