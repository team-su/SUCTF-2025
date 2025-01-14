use anchor_lang::prelude::*;

mod instructions;
mod states;

use instructions::*;
use states::*;

declare_id!("SUWsfWnuVp7cqPEMgndNdAou25h3SRXmKHzuRgaCZHU");

#[program]
pub mod checkin {
    use super::*;

    pub fn you_have_found(ctx: Context<Checkin>) -> Result<()> {
        ctx.accounts.checkin()
    }
}
