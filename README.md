# CodeXero Auto Bot

Automated bot for CodeXero Cluster Points Program that handles daily tasks and point tracking.

🔗 **Register here:** [https://www.codexero.xyz?referrer=CX-7TR1MX](https://www.codexero.xyz?referrer=CX-7TR1MX)

## Features

- ✅ Automatic login with wallet signature
- ✅ Daily task automation (daily-visit-app)
- ✅ Points tracking and monitoring
- ✅ Multi-account support
- ✅ Proxy support (optional)
- ✅ Auto-retry with 24-hour cycle
- ✅ Colorful console output
- ✅ WIB timezone support

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/febriyan9346/CodeXero-Auto-Bot.git
cd CodeXero-Auto-Bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure your accounts:
   - Edit `accounts.txt` and add your wallet private keys (one per line)
   - (Optional) Edit `proxies.txt` and add your proxies (one per line)

## Configuration

### accounts.txt
Add your Ethereum wallet private keys, one per line:
```
0x1234567890abcdef...
0xabcdef1234567890...
```

⚠️ **Security Warning:** Never share your private keys! Keep `accounts.txt` private and never commit it to public repositories.

### proxies.txt (Optional)
Add proxies in the following formats:
```
http://username:password@ip:port
http://ip:port
socks5://username:password@ip:port
```

If `proxies.txt` is empty or doesn't exist, the bot will run without proxies.

## Usage

Run the bot:
```bash
python bot.py
```

The bot will:
1. Load all accounts from `accounts.txt`
2. Load proxies from `proxies.txt` (if available)
3. Process each account:
   - Login with wallet signature
   - Claim daily task rewards
   - Check and display points
4. Wait 24 hours before the next cycle

## Output Example

```
CODEXERO AUTO BOT
════════════════════════════════════════════════════════════

[12:34:56] [INFO] Loaded 3 accounts successfully
[12:34:56] [CYCLE] Cycle #1 Started
[12:34:56] [INFO] Account #1/3
[12:34:56] [INFO] Wallet: 0x1234...5678 | Proxy: No Proxy
[12:34:57] [SUCCESS] Login berhasil!
[12:34:57] [INFO] Processing Task:
[12:34:58] [SUCCESS] Claim Sukses! Reward: +100 Points
[12:35:01] [SUCCESS] Total Points: 1,500 | Today: +100
```

## Features Breakdown

### Multi-Account Management
- Process multiple wallets automatically
- Each account processes independently
- Success/failure tracking per account

### Proxy Support
- Automatic proxy rotation
- Support for HTTP/HTTPS/SOCKS5
- Fallback to direct connection if proxy fails

### Smart Task Management
- Automatic daily task claiming
- Duplicate claim detection
- Error handling and retry logic

### Point Tracking
- Real-time point monitoring
- Daily earnings display
- Total points accumulation

## Troubleshooting

### Common Issues

**"File accounts.txt not found"**
- Create `accounts.txt` in the same directory as `bot.py`
- Add at least one private key

**"Login failed"**
- Check if your private key is correct
- Ensure your wallet is registered on CodeXero
- Try without proxy first

**"Task already claimed"**
- This is normal - tasks can only be claimed once per day
- The bot will try again in the next cycle

**Proxy Issues**
- Verify proxy format is correct
- Test proxy connection separately
- Try running without proxy first

## Security Notes

- ⚠️ **NEVER** share your private keys
- ⚠️ Keep `accounts.txt` secure and private
- ⚠️ Add `accounts.txt` to `.gitignore`
- ⚠️ Use a separate wallet for automated tasks
- ⚠️ Review the code before running

## Disclaimer

This bot is for educational purposes only. Use at your own risk. The author is not responsible for any losses or damages caused by using this bot.

- Always comply with CodeXero's Terms of Service
- Automated activities may be against platform rules
- Use responsibly and at your own discretion

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

If you find this bot helpful, consider:
- ⭐ Starring this repository
- 🔗 Using the referral link: [https://www.codexero.xyz?referrer=CX-7TR1MX](https://www.codexero.xyz?referrer=CX-7TR1MX)
- 🐛 Reporting bugs or issues
- 💡 Suggesting new features

## Contact

For questions or issues, please open an issue on GitHub.

---

**Happy Farming! 🚀**