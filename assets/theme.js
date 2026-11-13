/* Trade Charts – apply the saved light/dark choice before first paint (no saved choice = follow the OS). */
(function () { try { var t = localStorage.getItem('tc.theme'); if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t); } catch (e) {} })();
