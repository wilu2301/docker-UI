interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

export class CacheService {
  private static cache = new Map<string, CacheEntry<any>>();
  private static ttl = 1000 * 60 * 20;
  private static STORAGE_KEY = "cache";

  static init(): void {
    try {
      const storedCache = localStorage.getItem(this.STORAGE_KEY);
      if (storedCache) {
        const parsedCache = JSON.parse(storedCache);

        Object.entries(parsedCache).forEach(([key, entry]) => {
          if (Date.now() - (entry as CacheEntry<any>).timestamp <= this.ttl) {
            this.cache.set(key, entry as CacheEntry<any>);
          }
        });
      }
    } catch (error) {
      console.error("Failed to load cache from localStorage:", error);
    }
  }

  private static saveToStorage(): void {
    try {
      const cacheObject = Object.fromEntries(this.cache.entries());
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(cacheObject));
    } catch (error) {
      console.error("Failed to save cache to localStorage:", error);
    }
  }

  static get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;

    const now = Date.now();
    if (now - entry.timestamp > this.ttl) {
      this.delete(key);
      return null;
    }

    return entry.data;
  }

  static set<T>(key: string, data: T): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
    });
    this.saveToStorage();
  }

  static delete(key: string): void {
    this.cache.delete(key);
    this.saveToStorage();
  }

  static deleteAll(): void {
    this.cache.clear();
    this.saveToStorage();
  }
}

CacheService.init();
