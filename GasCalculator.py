import interactions

BOT_TOKEN = 'Your_Bot_Token' #Your Bot Token from discord applications
FOOTER_URL = 'https://cdn.discordapp.com/attachments/607052288842006534/1027893620747018240/Bitcoin_.jpg'

bot = interactions.Client(token=BOT_TOKEN)


def calculate_gas(price, amount, gas_limit, max_gas):
    gwei = []
    gas_price = []
    total_price = []
    avg_price = []
    for i in range(20):
        gwei.append(round((i + 1) * (float(max_gas) / 20)), 1)
        gas_price.append(round(float(gwei[i]) * float(gas_limit) / 1000000000, 4))
        total_price.append(round(float(price) * float(amount) + float(gas_price[i]), 4))
        avg_price.append(round((total_price[i] / float(amount)), 4))
    return gwei, total_price, avg_price


@bot.command(
    name="gas",
    description="Calculate gas",
    options=[
        interactions.Option(
            name="mint_price",
            description="Price per 1 NFT",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="amount",
            description="Amount",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="gas_limit",
            description="Gas Limit (200000 used by default)",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="max_gas",
            description="Max Gwei (100 used by default)",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def gas(ctx: interactions.CommandContext, mint_price=0.0, amount=1, gas_limit=200000, max_gas=100):
    fields = []
    footer = interactions.EmbedFooter(text='\tBy Dozerokz#2748', icon_url=FOOTER_URL)
    field1 = interactions.EmbedField(name='Mint Price', value=mint_price, inline=True)
    field2 = interactions.EmbedField(name='Amount', value=amount, inline=True)
    field3 = interactions.EmbedField(name='GasLimit', value=gas_limit, inline=True)
    fields.append(field1)
    fields.append(field2)
    fields.append(field3)

    gwei, gas_price, avg_price = calculate_gas(mint_price, amount, gas_limit, max_gas)

    field_gwei = interactions.EmbedField(name='Gwei', value='\n'.join(str(elem) for elem in gwei), inline=True)
    field_gas_price = interactions.EmbedField(name='Total Price', value='\n'.join(str(elem) for elem in gas_price),
                                              inline=True)
    field_total_price = interactions.EmbedField(name='Avg. Price', value='\n'.join(str(elem) for elem in avg_price),
                                                inline=True)
    fields.append(field_gwei)
    fields.append(field_gas_price)
    fields.append(field_total_price)

    embed = interactions.Embed(title='Gas Calculator', color=16777215, footer=footer, fields=fields)
    await ctx.send(embeds=embed)


if __name__ == '__main__':
    bot.start()
