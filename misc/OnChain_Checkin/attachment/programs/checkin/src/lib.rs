use anchor_lang::prelude::*;

mod instructions;
mod states;

use instructions::*;
use states::*;

declare_id!("SUCTF2Q25DnchainCheckin11111111111111111111");

#[program]
pub mod checkin {
    use super::*;

    pub fn flag2(ctx: Context<Checkin>) -> Result<()> {
        ctx.accounts.checkin()
    }
}
