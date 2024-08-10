export const getApiUrl = (): string => {
    return process.env.NEXT_PUBLIC_API_URL ?? 'https://url-not-set';
}