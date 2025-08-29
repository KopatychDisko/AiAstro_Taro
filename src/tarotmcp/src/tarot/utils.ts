// Use global crypto in Node.js >= 18 and browsers
declare const crypto: any;

/**
 * Generate a cryptographically secure random number between 0 and 1.
 * @throws {Error} If crypto.getRandomValues is not available.
 */
export function getSecureRandom(): number {
  if (typeof crypto !== 'undefined' && typeof crypto.getRandomValues === 'function') {
    const array = new Uint32Array(1);
    crypto.getRandomValues(array);
    return array[0] / (0xffffffff + 1);
  }
  throw new Error('A secure random number generator (crypto.getRandomValues) is not available in this environment.');
}